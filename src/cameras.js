export const cameras = [
  {
    id: "front-zed",
    label: "Front / ZED Camera",
    image_topic: "/zed/zed_node/rgb/image_rect_color/compressed",
    raw_image_topic: "/zed/zed_node/rgb/image_rect_color",
    camera_info_topic: "/zed/zed_node/rgb/camera_info",
    enabled: true,
    encoding: "compressed",
  },
];
