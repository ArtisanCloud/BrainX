import { useState, useEffect, useRef } from 'react';

const useCountdown = (initialSeconds: number, onCountdownEnd?: () => void) => {
	const [countdown, setCountdown] = useState(initialSeconds);
	const [started, setStarted] = useState(false);
	const timerRef = useRef<NodeJS.Timeout | null>(null); // 使用 useRef 存储计时器引用

	useEffect(() => {
		if (countdown === 0 && started) {
			onCountdownEnd?.();
			setStarted(false);
		}
	}, [countdown, started, onCountdownEnd]);

	useEffect(() => {
		if (started) {
			timerRef.current = setInterval(() => {
				setCountdown(prevCountdown => prevCountdown - 1);
			}, 1000);

			// 清除计时器
			return () => {
				if (timerRef.current) {
					clearInterval(timerRef.current);
					timerRef.current = null; // 清除引用
				}
			};
		}
	}, [started]);

	const startCountdown = (seconds: number) => {
		setCountdown(seconds);
		setStarted(true);
	};

	const stopCountdown = () => {
		setStarted(false);
		setCountdown(0);
		if (timerRef.current) {
			clearInterval(timerRef.current);
			timerRef.current = null; // 清除引用
		}
	};

	return { countdown, startCountdown, stopCountdown };
};

export default useCountdown;
