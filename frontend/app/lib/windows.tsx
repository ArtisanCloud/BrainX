import { useState, useEffect } from 'react';

interface WindowSize {
	width: number;
	height: number;
}

const useWindowSize = () => {
	const [size, setSize] = useState<WindowSize>({
		width: 0,
		height: 0,
	});

	const updateSize = () => {
		setSize({
			width: window.innerWidth,
			height: window.innerHeight,
		});
	};

	useEffect(() => {
		// 初次渲染时获取窗口尺寸
		updateSize();
		// 添加窗口大小变化监听事件
		window.addEventListener('resize', updateSize);

		// 组件卸载时清除监听事件
		return () => window.removeEventListener('resize', updateSize);
	}, []); // 只在组件挂载和卸载时执行

	return size;
};

export default useWindowSize;