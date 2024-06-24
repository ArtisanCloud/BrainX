export const FormatSSEMessageReply = (msg: string): string => {
	let objMsg = msg;
	if (objMsg === '') {
		objMsg = '\n';
	}
	objMsg = objMsg.replace(/\\n/g, '\n');

	return objMsg;
}
