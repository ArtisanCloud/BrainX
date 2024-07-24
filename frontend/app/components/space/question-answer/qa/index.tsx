import styles from './index.module.scss';
import {ActionQAQuery, RequestAQQuery} from "@/app/api/question-answer/query";
import classnames from "classnames";
import {Fragment, useContext, useEffect, useState} from "react";

import {Form, Button, Divider, Input, FormProps, Typography} from 'antd';
import useCountdown from "@/app/lib/countdown";
import {SelectLLMContext, SelectLLMContextType} from "@/app/components/space/provider/llm";

const {TextArea} = Input;

const QuestionAnswer = () => {
	const [answer, setAnswer] = useState<string>('');
	const {countdown, startCountdown, stopCountdown} = useCountdown(0); // 倒计时时间，单位为秒
	const {selectedLlm} = useContext(SelectLLMContext) as SelectLLMContextType;


	const secondsCountDown = 60

	const onFinish: FormProps<RequestAQQuery>["onFinish"] = async (values: RequestAQQuery) => {

		values.llm = selectedLlm!
		// console.log('Success:', values.question);
		try {
			// 如果提交验证成功，开始倒计时
			startCountdown(secondsCountDown)
			setAnswer('')
			const res = await ActionQAQuery(values);
			if (res.answer !== "") {
				// res.answer = "根据描述的问题中，绝缘胶带粘贴困难。所以可以推断出当前存在问题。为了解决这个问题，需要更多的信息来确定根本原因和永久解决方案。\n\n提供的约束条件为：无、两处挡墙过窄以及V3.0改为灌胶等细节。\n\n建议: 在考虑根因时，请确认绝缘胶带粘贴是否涉及到特定的材料或环境因素（例如湿度）引起的困难。如果是由这些原因导致的，可以考虑改进工作环境来解决这个问题，比如保持适当的温度和湿度。如果根本原因是由于材料质量差或是操作不正确导致的问题，建议重新培训相关工作人员并提供正确的工具和技术指导以确保绝缘胶带粘贴顺利进行。\n\n总之，在面对绝缘胶带粘贴困难时，需要进一步调查问题的根本原因，并根据具体情况给出适当的解决方案来解决这个问题。"
				setAnswer(res.answer);
			}
		} catch (error) {
			console.error("请求失败:", error);
		} finally {
			stopCountdown(); // 无论请求成功或失败，都停止倒计时
		}
	};

	const onFinishFailed: FormProps<RequestAQQuery>["onFinishFailed"] = (errorInfo: any) => {
		console.log('Failed:', errorInfo);
	};

	// 监听answer变量
	// useEffect(() => {
	// 	console.log("Answer changed:", answer);
	// }, [answer]); // 仅在 answer 发生变化时执行

	useEffect(() => {
		if (countdown === 0) {
			stopCountdown();
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [countdown]);


	return (
		<div className={styles.container}>
			<Form
				name="formQuestionAnswer"
				// initialValues={{remember: true}}
				onFinish={onFinish}
				onFinishFailed={onFinishFailed}
				autoComplete="off"
				// className={styles.form}
			>
				<Form.Item<RequestAQQuery>
					label="问题"
					name="question"
					rules={[{required: true, message: '请写下你的问题'}]}
				>
					<TextArea placeholder={"输入点什么你有兴趣的问题"} rows={4}/>
				</Form.Item>
				<Form.Item wrapperCol={{offset: 8, span: 16}}>
					<Button type="primary" htmlType="submit" disabled={countdown > 0}>
						{countdown > 0 ? `${countdown}s` : "提交"}
					</Button>
				</Form.Item>
			</Form>


			<div className={classnames(
				styles.result,
				{
					[styles.hide]: answer === ""
				}
			)}>
				<Divider orientation="left" className={styles.separate}>请看如下结果:</Divider>
				<Typography>
					{answer.split('\n').map((line, index) => (
						<Fragment key={index}>
							{line}
							{index !== answer.split('\n').length - 1 && <br/>}
						</Fragment>
					))}
				</Typography>
			</div>


		</div>
	);
}

export default QuestionAnswer;
