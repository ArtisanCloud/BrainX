import {App} from "@/app/api/robot-chat/app";

export const GetAppFromUUID = (uuid: string, apps: App[]): App | null => {
	// 遍历 apps 数组
	for (const app of apps) {
		// 检查当前代理对象的 uuid 是否与传入的 uuid 参数相匹配
		// console.log(app.uuid , uuid)
		if (app.uuid === uuid) {
			// 如果匹配，返回当前代理对象
			return app;
		}
	}
	// 如果未找到匹配的代理对象，则返回 null
	return null;
};
