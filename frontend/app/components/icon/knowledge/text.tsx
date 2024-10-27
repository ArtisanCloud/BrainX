// IconExample.js
import React from "react";
import {BlockOutlined} from "@ant-design/icons";


const IconText = ({ width = "24", height = "24", color = "currentColor" }) => (
    <BlockOutlined
      style={{fontSize: '32px', color: 'white', backgroundColor: '#5295e5'}}
      className="place-content-center rounded-lg border-1 w-full h-full"
    />
);

export default IconText;
