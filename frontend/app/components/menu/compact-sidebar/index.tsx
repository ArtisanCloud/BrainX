"use client";

import Image from "next/image";
import MenuLink from "@/app/components/menu/menu-link";
import styles from "./index.module.scss";
import {Button, Avatar} from "antd"
import {menuItems} from "@/app/components/menu";
import {LogoutOutlined} from '@ant-design/icons'
import {TbLayoutSidebarLeftExpandFilled} from "react-icons/tb";
import React, {useContext} from "react";
import {HideSidebarContext, SidebarContextType} from "@/app/components/menu/provider/sidebar-provider";
import Link from "next/link";
import {useRouter} from "next/navigation";
import useSessionStore from "@/app/store/session";

const CompactSidebar = () => {
  // const { user } = await auth();
  const router = useRouter();
  const {hideSidebar, setHideSidebar} = useContext(HideSidebarContext) as SidebarContextType;
  const {sessionLogout, user} = useSessionStore();

  const handleClickDrawerHandle = () => {
    setHideSidebar(!hideSidebar)
    // console.log(hideSidebar)
  }


  const handleSignOut = (event: any) => {
    sessionLogout()
    router.push('/')
  }

  return (
    <div className={styles.container}>
      <div className={styles.menu}>
        <div className={styles.user}>
          <Link href={"/"}>
            <Image
              className={styles.userImage}
              src={"/images/logo-s.png"}
              priority={true}
              alt=""
              width={50}
              height={50}
            />
          </Link>
        </div>
        <ul className={styles.list}>
          {menuItems.map((cat) => (
            <li key={cat.title}>
              {cat.list.map((item) => (
                <MenuLink item={item} key={item.title}/>
              ))}
            </li>
          ))}
        </ul>


      </div>
      <div className={styles.bottomBox}>
        <Avatar style={{
          marginTop: '20px',
          backgroundColor: '#af99d0',
          verticalAlign: 'middle',
          border: '#A283D2 solid 2px',
        }}
                size="small" gap={4}>
          {user?.account}
        </Avatar>

        <Button
          className={styles.logout}
          onClick={handleSignOut}
          danger
          size="small"
          icon={<LogoutOutlined/>}
        />
        <div className={styles.drawerHandler}>
          <TbLayoutSidebarLeftExpandFilled size={30} onClick={handleClickDrawerHandle}/>
        </div>
      </div>
    </div>
  );
};

export default CompactSidebar;
