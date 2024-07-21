import {ossUrl, staticsUrl} from "@/app/config/config";
import {App} from "@/app/api/app";
import {routeRobotChat} from "@/app/config/constant/index";

const notFoundImage = '/images/avatar-not-found.png'

export const GetPublicUrl = (resource: string | undefined) => {
	// console.log(resource)
	if (!resource) return notFoundImage;
	if (resource.startsWith('http://') || resource.startsWith('https://')) {
		return resource;
	}
	if (resource.startsWith('/')) {
		return resource;
	}
	return `/${resource}`;
};

export const GetOssUrl = (uri: string | undefined): string => {
	// console.log(uri)
	if (!uri) return notFoundImage;

	if (uri.startsWith('http://') || uri.startsWith('https://')) {
		return uri;
	}

	const normalizedUri = uri.startsWith('/') ? uri.slice(1) : uri;
	// console.log(ossUrl,normalizedUri)

	return `${ossUrl}/${normalizedUri}`;

};

export const GetStaticsUrl = (uri: string | undefined): string => {
	if (!uri) return notFoundImage;

	const normalizedUri = uri.startsWith('/') ? uri.slice(1) : uri;
	return `${staticsUrl}/${normalizedUri}`;

};



export const GetRobotChatUrlWithSpecificApp = (app: App) => {
	return routeRobotChat + `?app_uuid=${app.uuid}`
}
