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
}

const useSSE = () => {
  function handleError(err: Error, onerror: OnErrorCallback) {
    onerror(err);
  }

  function connectEventSource(options: EventSourceOptions) {
    const { method, url, body } = options;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    const token = Cookies.get(token_key)
    // console.log("connect:",token)
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const requestOptions: FetchEventSourceInit = {
      method: 'GET',
      headers,
      // signal: ctrl.signal,
      async onopen(response) {
        try {
          if (
            response.ok &&
            response.headers.get('content-type') === EventStreamContentType
          ) {
            options.onopen(response);
          } else if (
            response.status >= 400 &&
            response.status < 500 &&
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
        options.onclose();
      },
      onerror(err) {
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
  }

  return {
    handleError,
    connectEventSource,
  };
};
export default useSSE;
