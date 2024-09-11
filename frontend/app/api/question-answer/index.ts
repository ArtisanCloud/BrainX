export interface Document{
	similarity: number
	text: string
	node_id: string
	metadata: any
}

export interface ImageDocument {
	image: string
	relative_document: Document
}
