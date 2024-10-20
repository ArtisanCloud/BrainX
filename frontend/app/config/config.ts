import {env} from "./env.mjs";

export const backendUrl = env.NEXT_PUBLIC_BACKEND_URL;
export const frontendUrl = env.NEXT_PUBLIC_FRONTEND_URL;

export const ossUrl = env.NEXT_PUBLIC_OSS_URL;
export const staticsUrl = env.NEXT_PUBLIC_STATICS_URL;

export const openApiPlatform = process.env.NEXT_PUBLIC_OPENAPI_PLATFORM;
export const openApiKey = process.env.NEXT_PUBLIC_OPENAPI_ACCESS_KEY;
export const openApiSecret = process.env.NEXT_PUBLIC_OPENAPI_ACCESS_SECRET;

// console.log("****** current env url info:",backendUrl, frontendUrl)
// console.log("****** current env openApiKey info:",openApiKey)
