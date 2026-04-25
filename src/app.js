import { cameras } from "./cameras.js";

const bridgeUrlInput = document.querySelector("#bridge-url");
const connectButton = document.querySelector("#connect-button");
const bridgeStatus = document.querySelector("#bridge-status");
const cameraGrid = document.querySelector("#camera-grid");

let ros = null;
let subscriptions = [];
const cameraViews = new Map();
const objectUrls = new Map();

function setBridgeState(state, label) {
  bridgeStatus.textContent = label;
  bridgeStatus.className = `status-pill status-${state}`;
}

function setCameraState(cameraId, state, label) {
  const view = cameraViews.get(cameraId);
  if (!view) return;

  view.status.textContent = label;
  view.card.dataset.state = state;
}

function compressedImageToUrl(message) {
  if (typeof message.data === "string") {
    return `data:image/jpeg;base64,${message.data}`;
  }

  if (Array.isArray(message.data)) {
    const bytes = new Uint8Array(message.data);
    return URL.createObjectURL(new Blob([bytes], { type: "image/jpeg" }));
  }

  return "";
}

function renderCameraCards() {
  cameraGrid.innerHTML = "";
  cameraViews.clear();

  cameras
    .filter((camera) => camera.enabled)
    .forEach((camera) => {
      const card = document.createElement("article");
      card.className = "camera-card";
      card.dataset.state = "offline";

      const title = document.createElement("h2");
      title.textContent = camera.label;

      const status = document.createElement("span");
      status.className = "camera-status";
      status.textContent = "Offline";

      const viewport = document.createElement("div");
      viewport.className = "camera-viewport";

      const image = document.createElement("img");
      image.alt = `${camera.label} stream`;

      const placeholder = document.createElement("div");
      placeholder.className = "camera-placeholder";
      placeholder.textContent = "Waiting for frames";

      const topic = document.createElement("p");
      topic.className = "topic-line";
      topic.textContent = camera.image_topic;

      viewport.append(image, placeholder);
      card.append(title, status, viewport, topic);
      cameraGrid.append(card);

      cameraViews.set(camera.id, { card, image, placeholder, status });
    });
}

function stopSubscriptions() {
  subscriptions.forEach((topic) => topic.unsubscribe());
  subscriptions = [];

  objectUrls.forEach((url) => URL.revokeObjectURL(url));
  objectUrls.clear();
}

function disconnectRos() {
  stopSubscriptions();

  if (ros) {
    ros.close();
    ros = null;
  }

  cameras.forEach((camera) => setCameraState(camera.id, "offline", "Offline"));
  setBridgeState("offline", "Offline");
}

function subscribeToCamera(camera) {
  const view = cameraViews.get(camera.id);
  if (!view) return;

  setCameraState(camera.id, "loading", "Loading");

  // The ZED ROS2 driver publishes camera frames to ROS image topics.
  // This UI is a subscriber through rosbridge; it never publishes frames or
  // manually invokes a camera publisher. Future cameras only need config
  // entries with their image and camera_info topics.
  const topic = new ROSLIB.Topic({
    ros,
    name: camera.image_topic,
    messageType: "sensor_msgs/msg/CompressedImage",
  });

  let staleTimer = null;
  const markStaleLater = () => {
    window.clearTimeout(staleTimer);
    staleTimer = window.setTimeout(() => {
      setCameraState(camera.id, "stale", "No recent frames");
    }, 3000);
  };

  topic.subscribe((message) => {
    const previousUrl = objectUrls.get(camera.id);
    if (previousUrl) URL.revokeObjectURL(previousUrl);

    const imageUrl = compressedImageToUrl(message);
    if (!imageUrl) {
      setCameraState(camera.id, "stale", "Invalid frame");
      return;
    }

    if (imageUrl.startsWith("blob:")) objectUrls.set(camera.id, imageUrl);
    view.image.src = imageUrl;
    view.placeholder.hidden = true;
    setCameraState(camera.id, "online", "Live");
    markStaleLater();
  });

  subscriptions.push(topic);
}

function connectRos() {
  disconnectRos();

  const bridgeUrl = bridgeUrlInput.value.trim();
  if (!bridgeUrl) {
    setBridgeState("offline", "Missing URL");
    return;
  }

  setBridgeState("loading", "Connecting");
  ros = new ROSLIB.Ros({ url: bridgeUrl });

  ros.on("connection", () => {
    setBridgeState("online", "Connected");
    cameras.filter((camera) => camera.enabled).forEach(subscribeToCamera);
  });

  ros.on("error", () => {
    setBridgeState("offline", "Bridge error");
    cameras.forEach((camera) => setCameraState(camera.id, "offline", "Offline"));
  });

  ros.on("close", () => {
    setBridgeState("offline", "Disconnected");
    cameras.forEach((camera) => setCameraState(camera.id, "offline", "Offline"));
  });
}

renderCameraCards();
connectButton.addEventListener("click", connectRos);
window.addEventListener("beforeunload", disconnectRos);
