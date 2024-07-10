import type {NextRequest} from 'next/server'
import {token_key} from "@/app/lib/auth";

export function middleware(request: NextRequest) {
	const isAuthPath = request.nextUrl.pathname.startsWith('/user');
	const isHomePage = request.nextUrl.pathname === '/';

	const currentUserToken = request.cookies.get(token_key)?.value
	// console.log( currentUserToken)

	if (!currentUserToken && !isAuthPath && !isHomePage) {
		return Response.redirect(new URL('/user/login', request.url))
	}
}

export const config = {
	matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
