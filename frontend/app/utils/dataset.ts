import {DatasetImportType} from "@/app/api/knowledge/dataset";
import {ContentType} from "@/app/utils/media";

export const AllowedFileTypes = [
	ContentType.PDF,
	ContentType.DOC,
	ContentType.DOCX,
	ContentType.TXT,
	ContentType.MD,
	'.pdf',
	'.doc',
	'.docx',
	'.txt',
	'.md'
];

export const segmentationOptions = [
	{ value: '\n', label: '换行' },
	{ value: '\n\n', label: '两个换行' },
	{ value: '。', label: '中文句号' },
	{ value: '！', label: '中文感叹号' },
	{ value: '.', label: '英文句号' },
	{ value: '!', label: '英文感叹号' },
	{ value: '？', label: '中文问号' },
	{ value: '?', label: '英文问号' },
	// { value: '\n', label: 'Line break' },
	// { value: '\n\n', label: '2 line breaks' },
	// { value: '。', label: 'Chinese period' },
	// { value: '！', label: 'Chinese exclamation mark' },
	// { value: '.', label: 'English period' },
	// { value: '!', label: 'English exclamation mark' },
	// { value: '？', label: 'Chinese question mark' },
	// { value: '?', label: 'English question mark' },










];


export const getDatasetImportTypeTranslation = (type: DatasetImportType): string => {
	// console.log(type)
	switch (type) {
		case DatasetImportType.LOCAL_DOCUMENT:
			return '本地文档';
		case DatasetImportType.ONLINE_DATA:
			return '在线数据';
		case DatasetImportType.NOTION:
			return 'Notion';
		case DatasetImportType.GOOGLE_DOC:
			return 'Google文档';
		case DatasetImportType.LARK:
			return '飞书';
		case DatasetImportType.CUSTOM:
			return '自定义';
		default:
			return '未知类型';
	}
}
