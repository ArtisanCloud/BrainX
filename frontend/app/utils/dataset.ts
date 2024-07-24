import {DatasetImportType} from "@/app/api/knowledge/dataset";

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
