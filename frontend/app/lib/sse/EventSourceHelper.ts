import {
  EventStreamContentType,
  fetchEventSource,
  FetchEventSourceInit,
} from '@microsoft/fetch-event-source';
import FatalError from './FatalError';
import RetriableError from './RetriableError';
import Cookies from "js-cookie";
import {token_key} from "@/app/utils/auth";

type OnOpenCallback = (response: Response) => void;
type OnMessageCallback = (msg: any) => void;
type OnCloseCallback = () => void;
type OnErrorCallback = (err: Error) => void;

type RequestMethod = 'GET' | 'POST';

interface EventSourceOptions {
  method: RequestMethod;
  url: string;
  body?: any;
  onopen: OnOpenCallback;
  onmessage: OnMessageCallback;
  onclose: OnCloseCallback;
  onerror: OnErrorCallback;
  token?: string;
}

const useSSE = () => {
  function handleError(err: Error, onerror: OnErrorCallback) {
    onerror(err);
  }

  function getSSEAccessToken() {
    const token = Cookies.get(token_key)
    return token
  }

  function connectEventSource(options: EventSourceOptions) {
    const { method, url, body } = options;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    let token = getSSEAccessToken()
    // console.log('getSSEAccessToken', token);
    if (options.token !="" && options.token != undefined){
      token = options.token
    }
    // console.log("options.token:",token)
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    // 创建一个 AbortController 实例用于控制连接
    const controller = new AbortController();
    const { signal } = controller;

    const requestOptions: FetchEventSourceInit = {
      method: 'GET',
      headers,
      signal,
      // signal: ctrl.signal,
      async onopen(response) {
        // console.log('inner onopen', response);
        try {
          if (
            response.ok &&
            response.headers.get('content-type') === EventStreamContentType
          ) {
            options.onopen(response);
          } else if (
            response.status >= 400 &&
            response.status <= 500 &&
            response.status !== 429
          ) {
            throw new FatalError();
          } else {
            throw new RetriableError();
          }
        } catch (err: any) {
          handleError(err, options.onerror);
        }
      },
      onmessage(msg) {
        // console.log('inner onmessage', msg);
        try {
          if (msg.event === 'FatalError') {
            throw new FatalError(msg.data);
          } else {
            options.onmessage(msg);
          }
        } catch (err: any) {
          handleError(err, options.onerror);
        }
      },
      onclose() {
        console.log('inner onclose');
        options.onclose();
      },
      onerror(err) {
        console.log('inner onerror', err);
        options.onerror(err)
        throw err;

        if (err instanceof FatalError) {
          throw err;
        } else {
          // do nothing to automatically retry. You can also
          // return a specific retry interval here.
        }
      },
    };

    if (method === 'POST') {
      requestOptions.method = method;
      requestOptions.body = JSON.stringify(body);
    }
    // console.log(requestOptions);

    fetchEventSource(url, requestOptions);

    // 返回中止控制器，以便在外部调用
    return controller;
  }

  return {
    handleError,
    connectEventSource,
  };
};
export default useSSE;
