import Card from '@/app/components/dashboard/card/card';
import Chart from "@/app/components/dashboard/chart/chart";
import styles from "@/app/components/index.module.scss";
import Rightbar from "@/app/components/dashboard/rightbar/rightbar";
import Transactions from "@/app/components/dashboard/transactions/transactions";

import {
	fetchCardData
} from '@/app/lib/data';

export default async function DashboardPage() {
	const cards = await fetchCardData();

	// console.log(revenue)
	return (
		<div className={styles.wrapper}>
			<div className={styles.main}>
				<div className={styles.cards}>
					{cards.map((item:any) => (
						<Card item={item} key={item.id} />
					))}
				</div>
				<Transactions />
				<Chart />
			</div>
			<div className={styles.side}>
				<Rightbar />
			</div>
		</div>
	);
}
