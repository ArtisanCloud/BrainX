import type {NextRequest} from 'next/server'

export function middleware(request: NextRequest) {
	const isAuthPath = request.nextUrl.pathname.startsWith('/user');
	const isHomePage = request.nextUrl.pathname === '/';

	const currentUser = request.cookies.get('currentUser')?.value
	console.log(currentUser)
	// if (currentUser && !request.nextUrl.pathname.startsWith('/dashboard')) {
	// 	return Response.redirect(new URL('/dashboard', request.url))
	// }


	if (!currentUser && !isAuthPath && !isHomePage) {
		return Response.redirect(new URL('/user/login', request.url))
	}
}

export const config = {
	matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
