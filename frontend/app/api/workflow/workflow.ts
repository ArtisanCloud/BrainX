import {PowerModel} from "@/app/api";

export interface Workflow extends PowerModel {
  tenant_uuid: string
  app_uuid: string
  created_user_by: string
  updated_user_by: string
  parent_uuid: string
  name: string
  tag: string
  description: string
  type: number
  graph: string
  meta: string
}
