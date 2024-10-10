import {backendUrl, frontendUrl, openApiKey, openApiPlatform, openApiSecret} from "@/app/config/config";
import {notification} from 'antd';
import {Response as APIResponse} from "@/app/api";
import Cookies from "js-cookie";
import {openapi_token_key, token_key} from "@/app/utils/auth";
import {sleep} from "@/app/lib/base";
import {ResponseLogin, Token} from "@/app/api/auth";

interface ValidateError {
  type: string;
  loc: string[];
  msg: string;
  input: any;
  url: string;
}

interface ValidateErrorResponse {
  detail: ValidateError[];
}

class BackendClient {
  private isFetchingToken = false;  // 防止并发多次获取 token

  // 获取 token，如果不存在则请求新的 token
  private async getToken() {
    let token = Cookies.get(openapi_token_key);
    // console.log("cookie token:", token)
    if (!token && !this.isFetchingToken) {
      this.isFetchingToken = true; // 标记正在获取 token
      try {
        const newToken = await this.fetchNewToken(); // 获取新的 token
        // console.log("new token:", newToken)
        Cookies.set(openapi_token_key, newToken.access_token);  // 保存 token
        token = newToken.access_token;
      } catch (error) {
        notification.error({
          message: '获取 token 失败',
          description: '请检查 OpenAPI Key 和 Secret 是否正确。',
          duration: 3,
        });
      } finally {
        this.isFetchingToken = false; // 重置状态
      }
    }
    return token;
  }

  // 发送 openApiKey 和 openApiSecret 获取新的 token
  private async fetchNewToken(): Promise<Token> {
    const response = await fetch(`${backendUrl}/openapi/v1/auth`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        platform: openApiPlatform,
        access_key: openApiKey,
        secret_key: openApiSecret,
      }),
    });
    // console.log(response)
    const result = await response.json();
    // console.log(result)
    if (response.ok && result.token) {
      return result.token;
    } else {
      throw new Error('获取 token 失败');
    }
  }

  // 获取 header 并自动添加 token
  private async get_header() {
    const token = await this.getToken();

    const headers: any = {
      "Content-Type": "application/json",
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  public async backend_get(endpoint: string, init?: any) {
    return this.get(backendUrl, endpoint, init);
  }

  public async backend_post(endpoint: string, body?: any) {
    return this.post(backendUrl, endpoint, body);
  }

  public async backend_patch(endpoint: string, body?: any) {
    return this.patch(backendUrl, endpoint, body);
  }

  public async backend_delete(endpoint: string, body?: any) {
    return this.delete(backendUrl, endpoint, body);
  }

  public async frontend_get(endpoint: string, init?: any) {
    return this.get(frontendUrl, endpoint, init);
  }

  public async frontend_post(endpoint: string, body?: any) {
    return this.post(frontendUrl, endpoint, body);
  }

  // 公共 GET 请求
  public async get(host: string, endpoint: string, init?: any): Promise<any> {
    const url = host + endpoint;
    const headers = init?.headers ? {...(await this.get_header()), ...init.headers} : await this.get_header();
    const newInit = {...init, headers};
    const res = await fetch(url, newInit);

    return this.processResponse(res);
  }

  // 公共 POST 请求
  public async post(host: string, endpoint: string, body?: any): Promise<any> {
    const url = host + endpoint;
    const res = await fetch(url, {
      method: "POST",
      headers: await this.get_header(),
      body: JSON.stringify(body),
    });

    return this.processResponse(res);
  }

  // 公共 PATCH 请求
  public async patch(host: string, endpoint: string, body?: any): Promise<any> {
    const url = host + endpoint;
    const res = await fetch(url, {
      method: "PATCH",
      headers: await this.get_header(),
      body: JSON.stringify(body),
    });

    return this.processResponse(res);
  }

  // 公共 DELETE 请求
  public async delete(host: string, endpoint: string, body?: any): Promise<any> {
    const url = host + endpoint;
    const res = await fetch(url, {
      method: "DELETE",
      headers: await this.get_header(),
      body: JSON.stringify(body),
    });

    return this.processResponse(res);
  }

  private async processHttpErrorResponse(res: Response) {
    if (res.status == 422) {
      const errorResponse = await res.json() as ValidateErrorResponse;
      const errors = errorResponse.detail;
      errors.map((error) => {
        notification.warning({
          message: error.msg,
          description: `${error.loc.join(": ")} ${JSON.stringify(error.input)}`,
        });
      });
    } else if (res.status == 401) {
      notification.error({
        message: "当前未登录状态",
        description: "需要重新登录",
        duration: 3,
      });
      return;
    }
  }

  private async processStatusErrorResponse(result: APIResponse) {
    notification.error({
      message: result.error,
      description: result.detail,
    });
  }

  private async processResponse(res: Response) {
    if (!res.ok) {
      await this.processHttpErrorResponse(res);
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const result = (await res.json()) as APIResponse;
    if (result.error) {
      await this.processStatusErrorResponse(result);
      throw new Error(`Request error: ${result.error}`);
    }

    return result;
  }
}

export const backendClient = new BackendClient();
