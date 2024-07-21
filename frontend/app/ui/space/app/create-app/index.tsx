"use client";

import styles from './index.module.scss'
import {useContext, useState} from "react";
import {LoadingOutlined, PlusOutlined} from '@ant-design/icons';
import {Input, message, Upload} from 'antd';
import type {GetProp, UploadProps} from 'antd';

import Image from 'next/image';
import {CreateAppContext, CreateAppContextType} from "@/app/ui/space/app/provider/create-app-provider";
import {GetOssUrl} from "@/app/lib/url";
import {
	ActionCreateMediaResource, bucket_name,
	RequestCreateMediaResource,
	ResponseCreateMediaResource
} from "@/app/api/media-resource";

const {TextArea} = Input;

const CreateApp = () => {
	const {
		name,
		setName,
		description,
		setDescription,
		avatarUrl,
		setAvatarUrl
	} = useContext(CreateAppContext) as CreateAppContextType;


	const [loading, setLoading] = useState(false);

	type FileType = Parameters<GetProp<UploadProps, 'beforeUpload'>>[0];

	const getBase64 = (img: FileType, callback: (url: string) => void) => {
		const reader = new FileReader();
		reader.addEventListener('load', () => callback(reader.result as string));
		reader.readAsDataURL(img);
	};

	const beforeUpload = (file: FileType) => {
		const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
		if (!isJpgOrPng) {
			message.error('You can only upload JPG/PNG file!');
		}
		const isLt2M = file.size / 1024 / 1024 < 2;
		if (!isLt2M) {
			message.error('Image must smaller than 2MB!');
		}
		return isJpgOrPng && isLt2M;
	};

	const handleChange: UploadProps['onChange'] = async (info) => {
		if (info.file.status === 'uploading') {
			setLoading(true);
			return;
		}
		if (info.file.status === 'done') {
			// Get this url from response in real world.
			getBase64(info.file.originFileObj as FileType, async (base64) => {
				const requestData = {
					mediaName: info.file.name,
					bucketName: bucket_name,
					base64Data: base64
				} as RequestCreateMediaResource
				const res:ResponseCreateMediaResource = await ActionCreateMediaResource(requestData, 0);
				// console.log(res)
				if (res) {
					setLoading(false);
					// console.log(res.media_resource)
					setAvatarUrl(res.media_resource.url);
				}
			});
		}
	};

	const handleChangeName = (e: any) => {
		setName(e.target.value)
	}
	const handleChangeDescription = (e: any) => {
		setDescription(e.target.value)

	}

	const uploadButton = (
		<button style={{border: 0, background: 'none'}} type="button">
			{loading ? <LoadingOutlined/> : <PlusOutlined/>}
			<div style={{marginTop: 8}}>Upload</div>
		</button>
	);

	return (
		<div className={styles.container
		}>
			<div className={styles.form}>
				<div className={styles.name}>
					<div className={styles.title}>机器人名称</div>
					<div>
						<Input onChange={handleChangeName} value={name!} placeholder={"为机器人设定一个唯一名称"}/>
					</div>
				</div>
				<div className={styles.description}>
					<div className={styles.title}>机器人描述</div>
					<div>
						<TextArea onChange={handleChangeDescription} value={description!}
											placeholder={"请对该代理机器人，进行一些功能特征上的描述"} rows={4}/>
					</div>
				</div>
				<div className={styles.avatar}>
					<Upload
						name="avatar"
						listType="picture-card"
						className="avatar-uploader"
						showUploadList={false}
						beforeUpload={beforeUpload}
						onChange={handleChange}
					>
						{avatarUrl ? <Image
							src={GetOssUrl(avatarUrl)}
							className={'rounded-lg'}
							alt="avatar"
							priority
							width={80}
							height={80}
							style={{width: '100%', height: '100%',}}/> : uploadButton}
					</Upload>
				</div>
			</div>

		</div>
	)
}
export default CreateApp
