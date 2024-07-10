import type {NextRequest} from 'next/server'
import {getToken} from "@/app/lib/auth";

export function middleware(request: NextRequest) {
	const isAuthPath = request.nextUrl.pathname.startsWith('/user');
	const isHomePage = request.nextUrl.pathname === '/';

	const currentUserToken = getToken()
	console.log(currentUserToken)
	// if (currentUser && !request.nextUrl.pathname.startsWith('/dashboard')) {
	// 	return Response.redirect(new URL('/dashboard', request.url))
	// }


	if (!currentUserToken && !isAuthPath && !isHomePage) {
		return Response.redirect(new URL('/user/login', request.url))
	}
}

export const config = {
	matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
