import Card from '@/app/ui/dashboard/card/card';
import Chart from "@/app/ui/dashboard/chart/chart";
import styles from "@/app/ui/index.module.scss";
import Rightbar from "@/app/ui/dashboard/rightbar/rightbar";
import Transactions from "@/app/ui/dashboard/transactions/transactions";

import {
	fetchRevenue, fetchLatestInvoices,fetchCardData} from '@/app/lib/data';

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