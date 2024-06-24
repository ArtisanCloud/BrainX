
export interface Conversation {
	currentPrompt: string;
	items: ConversationItem[];

}

export interface ConversationItem {
	question: string;
	answer: string;
}