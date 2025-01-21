"use client";

import Image from "next/image";
import MenuLink from "@/app/components/menu/menu-link";
import styles from "./index.module.scss";
import { TbLayoutSidebarRightExpand } from "react-icons/tb";
import {LogoutOutlined} from '@ant-design/icons'
import {Avatar} from 'antd';
import {Form} from "antd"
import {menuItems} from "@/app/components/menu";
import React, {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/components/menu/provider/sidebar-provider";
import Link from "next/link";
import {useRouter} from "next/navigation";
import useSessionStore from "@/app/store/session";


const Sidebar = () => {
  // const { user } = await auth();
  const {hideSidebar, setHideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
  const {  sessionLogout, user} = useSessionStore();

  const handleClickDrawerHandle = () => {
    setHideSidebar(!hideSidebar)
  }

  const router = useRouter();

  const handleSignOut = (event: any) => {
    sessionLogout()
    router.push('/')
  }

  return (
    <div className={styles.container}>
      <div className={styles.menu}>
        <Link
          href="/"
        >
          <div className={styles.user}>
            <Image
              className={styles.userImage}
              // src={user.img || "/noavatar.png"}
              src={"/images/logo-s.png"}
              priority={true}
              alt=""
              width="50"
              height="50"
            />
            <div className={styles.userDetail}>
              {/*<span className={styles.username}>{user.username}</span>*/}
              <span className={styles.userTitle}>BrainX</span>
            </div>
          </div>
        </Link>
        <ul className={styles.list}>
          {menuItems.map((cat) => (
            <li key={cat.title}>
              <span className={styles.cat}>{cat.title}</span>
              {cat.list.map((item) => (
                <MenuLink item={item} key={item.title}/>
              ))}
            </li>
          ))}
        </ul>
        <Form
          name="signout"
          onFinish={handleSignOut}
        >
          <button className={styles.logout}>
            <Avatar style={{
              backgroundColor: '#af99d0',
              verticalAlign: 'middle',
              border: '#A283D2 solid 2px',
            }}
                    size="small" gap={4}>
              {user?.account}
            </Avatar>
            <LogoutOutlined/> Logout
          </button>
        </Form>
      </div>
      <div className={styles.drawerHandler}>
        <TbLayoutSidebarRightExpand size={30}  onClick={handleClickDrawerHandle}/>
      </div>

    </div>
  );
};

export default Sidebar;
