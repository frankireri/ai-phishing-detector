"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { useState } from "react";
import { FiShield, FiMenu, FiX, FiUser, FiLogOut, FiBarChart2, FiHome, FiInfo } from "react-icons/fi";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Detector", icon: FiHome },
  { href: "/dashboard", label: "Dashboard", icon: FiBarChart2, protected: true },
  { href: "/analytics", label: "Analytics", icon: FiBarChart2, protected: true },
  { href: "/about", label: "About", icon: FiInfo },
];

export default function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const [menu, setMenu] = useState(false);

  return (
    <nav className="sticky top-0 z-40 backdrop-blur bg-white/80 border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="bg-primary-600 text-white p-2 rounded-lg group-hover:scale-105 transition-transform">
              <FiShield className="w-5 h-5" />
            </div>
            <div>
              <p className="font-bold text-slate-900 leading-none">PhishGuard AI</p>
              <p className="text-[10px] text-slate-500 leading-none mt-0.5">CUEA • Final Year Project</p>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {navItems
              .filter((it) => !it.protected || user)
              .map((it) => {
                const Icon = it.icon;
                const active = pathname === it.href;
                return (
                  <Link
                    key={it.href}
                    href={it.href}
                    className={cn(
                      "px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition",
                      active
                        ? "bg-primary-50 text-primary-700"
                        : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    {it.label}
                  </Link>
                );
              })}
          </div>

          <div className="hidden md:flex items-center gap-2">
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setMenu(!menu)}
                  className="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-slate-100 transition"
                >
                  <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center font-semibold">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-sm font-medium">{user.username}</span>
                </button>
                {menu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 py-1 animate-fade-in">
                    <Link
                      href="/dashboard"
                      onClick={() => setMenu(false)}
                      className="block px-4 py-2 text-sm hover:bg-slate-50"
                    >
                      Dashboard
                    </Link>
                    <button
                      onClick={() => {
                        setMenu(false);
                        logout();
                      }}
                      className="w-full text-left px-4 py-2 text-sm hover:bg-slate-50 text-red-600 flex items-center gap-2"
                    >
                      <FiLogOut className="w-4 h-4" />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link href="/login" className="btn-secondary">
                  Login
                </Link>
                <Link href="/register" className="btn-primary">
                  Sign Up
                </Link>
              </>
            )}
          </div>

          <button
            className="md:hidden p-2 rounded-md text-slate-600 hover:bg-slate-100"
            onClick={() => setOpen(!open)}
          >
            {open ? <FiX className="w-5 h-5" /> : <FiMenu className="w-5 h-5" />}
          </button>
        </div>

        {open && (
          <div className="md:hidden border-t border-slate-200 py-3 space-y-1">
            {navItems
              .filter((it) => !it.protected || user)
              .map((it) => (
                <Link
                  key={it.href}
                  href={it.href}
                  onClick={() => setOpen(false)}
                  className={cn(
                    "block px-3 py-2 rounded-md text-sm font-medium",
                    pathname === it.href
                      ? "bg-primary-50 text-primary-700"
                      : "text-slate-600 hover:bg-slate-100"
                  )}
                >
                  {it.label}
                </Link>
              ))}
            <div className="pt-2 border-t border-slate-200 mt-2 space-y-1">
              {user ? (
                <button
                  onClick={() => {
                    setOpen(false);
                    logout();
                  }}
                  className="block w-full text-left px-3 py-2 rounded-md text-sm text-red-600 hover:bg-red-50"
                >
                  Logout ({user.username})
                </button>
              ) : (
                <>
                  <Link
                    href="/login"
                    onClick={() => setOpen(false)}
                    className="block px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:bg-slate-100"
                  >
                    Login
                  </Link>
                  <Link
                    href="/register"
                    onClick={() => setOpen(false)}
                    className="block px-3 py-2 rounded-md text-sm font-medium bg-primary-600 text-white text-center"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
