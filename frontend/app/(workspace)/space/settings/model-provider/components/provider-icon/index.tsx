import React, { useEffect, useState } from "react";
import { ActionGetProviderIcon } from "@/app/api/model-provider/provider";
import Image from 'next/image';

// 缓存请求结果，避免重复请求
const iconCache: Record<string, string> = {};

interface ProviderIconProps {
  providerName: string;
  iconSize?: string;
}


export function ProviderIcon({
                               providerName, iconSize = 'icon_large'
}: ProviderIconProps) {
  const [icon, setIcon] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    async function fetchIcon() {
      if (loading){
        return
      } else{
        setLoading(true);
      }
      const cachedKay= providerName+'-'+iconSize
      if (iconCache[cachedKay]) {
        // 如果缓存中已有图标，直接使用缓存的图标
        setIcon(iconCache[cachedKay]);

        setLoading(false);
      } else {
        try {
          setLoading(true);
          const svg = await ActionGetProviderIcon(providerName,iconSize); // 使用优化后的缓存函数
          // console.log(svg)
          // 缓存 SVG 内容
          setIcon(svg);
          iconCache[cachedKay] = svg;
        } catch (error) {
          console.error("Failed to load provider icon:", error);
        } finally {
          setLoading(false);
        }
      }
    }

    fetchIcon();
  }, [providerName]);

  if (loading) {
    return <p>Loading...</p>;
  }

  // 判断返回的内容类型，如果是 URL，则认为是图片
  if (typeof icon === 'string' && icon.startsWith("blob:")) {
    return <Image width={42} height={42} className="w-auto h-6" src={icon} alt={`${providerName} Icon`} />;
  }

  // 如果是 SVG 内容，使用 dangerouslySetInnerHTML 渲染
  if (icon) {
    return <div className="w-auto h-6" dangerouslySetInnerHTML={{ __html: icon }} />;
  }
}
