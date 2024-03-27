import { Card } from '@/app/components/dashboard/cards';
import RevenueChart from '@/app/components/dashboard/revenue-chart';
import LatestInvoices from '@/app/components/dashboard/latest-invoices';
import { noto_serif } from '@/app/styles/fonts';
import { fetchRevenue } from '@/app/utils/data';

export default async function Page() {
	// const revenue = await fetchRevenue();
	// console.log(revenue)
	return (
		<main>
			<h1 className={`${noto_serif.className} mb-4 text-xl md:text-2xl`}>
				Dashboard
			</h1>
			<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
				{/* <Card title="Collected" value={totalPaidInvoices} type="collected" /> */}
				{/* <Card title="Pending" value={totalPendingInvoices} type="pending" /> */}
				{/* <Card title="Total Invoices" value={numberOfInvoices} type="invoices" /> */}
				{/* <Card
          title="Total Customers"
          value={numberOfCustomers}
          type="customers"
        /> */}
			</div>
			<div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-4 lg:grid-cols-8">
				{/* <RevenueChart revenue={revenue}  /> */}
				{/* <LatestInvoices latestInvoices={latestInvoices} /> */}
			</div>
		</main>
	);
}