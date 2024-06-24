import {PowerModel} from "@/app/api";

export interface Knowledge extends PowerModel{
	name: string;
	description: string;
	units: number;
	size: string
}