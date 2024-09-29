"use client";

import styles from './index.module.scss';

import {LeftOutlined, CopyOutlined} from '@ant-design/icons';
import {CogIcon} from '@heroicons/react/24/outline';


const TopBar = () => {
  return (
    <div className={styles.container}>
      <div className={styles.leftBox}>
        <div className={styles.backButton}>
          <LeftOutlined style={{fontSize: '16px', color: "#6b6b75"}}/>
        </div>
        <div className={styles.workflowAvatar}>
          <CogIcon style={{width: '24px', color: "white"}}/>
        </div>
        <div>
          <div className="flex items-center space-x-[2px]">
            <span
              className="semi-typography text-[#1d1c23] font-[600] leading-6 semi-typography-ellipsis semi-typography-ellipsis-single-line semi-typography-ellipsis-overflow-ellipsis semi-typography-ellipsis-overflow-ellipsis-text semi-typography-primary semi-typography-normal">
              <span>AIGMedia</span>
            </span>
            <div className="flex items-center justify-center w-4 h-4 hover:bg-[#0607091A] rounded-[4px]">
              <svg className="icon-icon icon-icon-coz_info_circle text-xs text-[#060709]/[50%]" width="1em" height="1em"
                   viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M12 21C16.9705 21 21 16.9705 21 12C21 7.02947 16.9705 2.99997 12 2.99997C7.0295 2.99997 3 7.02947 3 12C3 16.9705 7.0295 21 12 21ZM12 23C5.925 23 1 18.075 1 12C1 5.92497 5.925 0.999969 12 0.999969C18.075 0.999969 23 5.92497 23 12C23 18.075 18.075 23 12 23ZM11 15.5V11.5C10.4477 11.5 10 11.0523 10 10.5C10 9.94768 10.4477 9.49997 11 9.49997H12.0036C12.5545 9.49997 13.0017 9.94549 13.0025 10.4964C13.005 12.1642 13 13.8321 13 15.5H13.5C14.0523 15.5 14.5 15.9477 14.5 16.5C14.5 17.0523 14.0523 17.5 13.5 17.5L10.5 17.5C9.94772 17.5 9.5 17.0523 9.5 16.5C9.5 15.9477 9.94772 15.5 10.5 15.5H11ZM12 8.49997C11.4477 8.49997 11 8.05225 11 7.49997C11 6.94768 11.4477 6.49997 12 6.49997C12.5523 6.49997 13 6.94768 13 7.49997C13 8.05225 12.5523 8.49997 12 8.49997Z"></path>
              </svg>
            </div>
            <div className="flex items-center justify-center w-4 h-4 hover:bg-[#0607091A] rounded-[4px] cursor-pointer"
                 tabIndex="0" aria-describedby="6lkrfxg" data-popupid="6lkrfxg">
              <svg className="icon-icon icon-icon-coz_edit text-[#060709]/[50%] text-xs" width="1em" height="1em"
                   viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M19.2531 2.64649C19.8389 2.06071 20.7886 2.06071 21.3744 2.64649 21.9602 3.23228 21.9602 4.18203 21.3744 4.76781L20.3138 5.82847 18.1925 3.70715 19.2531 2.64649zM17.1392 4.76043L19.2605 6.88175 11.4426 14.6996C11.2337 14.9085 10.9647 15.0469 10.6732 15.0954L8.78231 15.4098C8.72828 15.4188 8.67325 15.4012 8.63453 15.3624 8.59531 15.3232 8.57774 15.2673 8.58748 15.2127L8.92316 13.3307C8.97322 13.05 9.10815 12.7915 9.30975 12.5899L17.1392 4.76043z"></path>
                <path
                  d="M13.5 3H4C2.89543 3 2 3.89543 2 5V20C2 21.1046 2.89543 22 4 22H19C20.1046 22 21 21.1046 21 20V10L19 12V20H4V5H11.5L13.5 3Z"></path>
              </svg>
            </div>
          </div>
          <div className="flex items-center text-xs h-4">
            <div className="semi-space semi-space-align-center semi-space-horizontal" x-semi-prop="children">
              <div className="px-[6px] rounded-[4px] bg-[#F0F0F5] text-[#1D1C2399] space-x-1">
                <span>Saved at 11:21:36</span></div>
            </div>
          </div>
        </div>
      </div>
      <div className={styles.rightBox}>
        <div className={styles.splitButton}>
          <button className={styles.testButton}>
            测试运行
          </button>
          <button className={styles.moreButton}>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"
                 focusable="false" aria-hidden="true">
              <path
                d="M20.5598 9.65618L12.7546 18.6322C12.3559 19.0906 11.644 19.0906 11.2453 18.6322L3.4401 9.65618C2.8773 9.00895 3.33701 8 4.19471 8L19.8052 8C20.6629 8 21.1226 9.00895 20.5598 9.65618Z"
                fill="currentColor"></path>
            </svg>
          </button>
        </div>
        <button className={styles.publishButton}>
          发布
        </button>
        <button className={styles.copyButton}>
          <CopyOutlined style={{fontSize: '16px', color: '#383743'}}/>
        </button>
      </div>

    </div>
  )
}

export default TopBar;
