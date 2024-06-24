export interface Document{
	text: string
	node_id: string
	metadata: any
}

export interface ImageDocument {
	image: string
	relative_document: Document
}