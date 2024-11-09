export interface SSEMessage {
  status: string
  content: string
  error: string
  message: string
}

export const FormatSSEMessageReply = (msg: string): string => {
  let objMsg = msg;
  if (objMsg === '' || objMsg == undefined) {
    objMsg = '\n';
  }
  objMsg = objMsg.replace(/\\n/g, '\n');

  return objMsg;
}
