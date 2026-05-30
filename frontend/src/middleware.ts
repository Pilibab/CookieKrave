import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/auth/login", "/auth/callback-loading"];
const IS_MOCK = process.env.NEXT_PUBLIC_MOCK === "true";

export function middleware(request: NextRequest) {
  // Mock mode: skip all auth checks so you can browse freely
  if (IS_MOCK) return NextResponse.next();

  const { pathname } = request.nextUrl;
  const isPublic = PUBLIC_PATHS.some((p) => pathname.startsWith(p));
  const hasSession = request.cookies.has("connect.sid") || request.cookies.has("session");

  if (!isPublic && !hasSession) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }
  if (isPublic && hasSession && pathname.startsWith("/auth/login")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
