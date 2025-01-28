import { ArrowRightIcon } from "@heroicons/react/24/outline";
import styles from "@/app/components/home/index.module.scss";
import HomeNavbar from "@/app/components/home/navbar";
import brainXImage from "/public/images/brainx.jpeg";
import { Button, Image, Link } from "@heroui/react";

export default function Home() {
  return (
    <main className={`${styles.container}`}>
      <HomeNavbar />
      <div className={"flex h-content bg-bodyDefault w-screen"}>
        <div className={"w-3/5 h-full flex flex-col justify-center pl-10"}>
          <p className={"text-4xl font-bold mb-0.5"}>欢迎使用BrainX.</p>
          <p className={"text-3xl font-bold"}>
            这是一个很有意思的网络知识系统，提供智能化系统，欢迎来体验。
          </p>
          <div className={"mt-3"}>
            <Link
              href="space/workspace/robot-chat"
              className="rounded opacity-75 bg-primary text-white px-4 py-2 flex justify-between gap-2 w-[120px] h-[40px]"
            >
              <span>开始</span>
              <ArrowRightIcon className={"text-white w-8 scale-75"} />
            </Link>
          </div>
        </div>
        <div className={"w-1/3 flex justify-center flex-col"}>
          <div className={"relative h-800 w-800 scale-50 -ml-52"}>
            <Image
              alt={"BrainX"}
              src={brainXImage.src}
              width={800}
              height={800}
              className={"absolute left-0 top-0 z-10 rounded-full"}
            />
            <div
              id={"card-item-bg"}
              style={
                {
                  "--image": `url(${brainXImage.src})`,
                  backgroundImage: `var(--image)`,
                  backgroundSize: "cover",
                  transition: "0.3s ease-in-out",
                } as React.CSSProperties
              }
              className={
                "absolute w-800 h-800 left-0 top-0 scale-105 soft-card-img hero-gradient blur-lg z-1 rounded-full"
              }
            />
          </div>
        </div>
      </div>
      <div className={styles.footer}>
        <span>Powered By ArtisanCloud</span>
      </div>
    </main>
  );
}
