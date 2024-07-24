import {PowerModel} from "@/app/api";

export interface DocumentSegment extends PowerModel {
	tenant_uuid?: string;
	document_uuid?: string;
	dataset_uuid?: string;
	created_user_by?: string;
	updated_user_by?: string;
	status?: number;
	content?: string;
	document_index?: number;
	word_count?: number;
	token_count?: number;
}
