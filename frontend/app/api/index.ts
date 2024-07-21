

export interface PowerModel {
	id?: number;
	uuid?: string;
	createdAt?: string;
	updatedAt?: string;
	deletedAt?: string;
}

export interface Response {
	error: string;
	detail: any;
	message: string
	data: any
	status_code: number
}

export interface imageAbleInfo {
	icon?: string;
	backgroundColor?: string;
	imageURL?: string;
}

export interface RequestPagination{
	page:number
	page_size:number
}

export interface ResponsePagination{
	page: number,
	per_page: number,
	sort: boolean,
	total_rows: number,
	total_pages: number,
}
