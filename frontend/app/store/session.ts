import { create } from 'zustand';
import { User } from "@/app/api/tenant/user";
import Cookies from 'js-cookie';
import { account_key, token_key } from "@/app/utils/auth";
import { Token } from "@/app/api/auth";

// 定义 Store 状态和操作
interface SessionState {
  user: User | null;  // 用户信息
  token: string | null; // 存储 token
  isLoggedIn: boolean;  // 登录状态
  sessionLogin: (user: User, token: Token) => void;  // 登录方法
  sessionLogout: () => void;  // 登出方法
}

// 创建 store
const useSessionStore = create<SessionState>((set) => ({
  user: null, // 初始化时用户为 null
  token: null, // 初始化时 token 为 null
  isLoggedIn: false, // 初始化时未登录

  // 登录方法
  sessionLogin: (user: User, token: Token) => {
    // 将用户信息和 token 存储到 cookie 中
    Cookies.set(token_key, token.access_token, { expires: token.expires_in / (60 * 60 * 24) }); // 设置 token 有效期为天数
    Cookies.set(account_key, JSON.stringify(user), { expires: 7 }); // 7天有效期
    set({
      user: user,
      token: token.access_token,
      isLoggedIn: true,
    });
  },

  // 登出方法
  sessionLogout: () => {
    // 清除 cookie 中的用户信息和 token
    Cookies.remove(account_key);
    Cookies.remove(token_key);
    set({
      user: null,
      token: null,
      isLoggedIn: false,
    });
  },
}));

export default useSessionStore;
