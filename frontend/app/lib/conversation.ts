import {ConversationItem, Message} from "@/app/api/robot-chat/conversation";

export const convertDataToConversationItems = (data: Message[]): ConversationItem[] => {
	const conversationItems: ConversationItem[] = [];

	let currentQuestion = '';
	let currentAnswer = '';

	for (const message of data) {
		if (message.type === 'human') {
			// 如果是 human 类型的 message，存储当前的 question，并重置 answer
			currentQuestion = message.content;
		} else if (message.type === 'AIMessageChunk') {
			// 如果是 AIMessageChunk 类型的 message，存储当前的 answer，并创建一个新的 ConversationItem
			currentAnswer = message.content;
			conversationItems.push({ question: currentQuestion, answer: currentAnswer });

			// 重置 currentQuestion 和 currentAnswer 为下一个可能的 question 和 answer
			currentQuestion = '';
			currentAnswer = '';
		}
	}

	// 如果还有剩余的 question 和 answer 没有被处理，最后一个单独处理
	if (currentQuestion !== '' || currentAnswer !== '') {
		conversationItems.push({ question: currentQuestion, answer: currentAnswer });
	}

	return conversationItems;
}
