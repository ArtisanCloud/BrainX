import {sql} from '@vercel/postgres';
import {
	CustomerField,
	CustomersTableType,
	InvoiceForm,
	InvoicesTable,
	LatestInvoiceRaw,
	User,
	Revenue,
} from './definitions';
import {formatCurrency} from './base';
import {unstable_noStore as noStore} from 'next/cache';
import {backendClient} from "@/app/api/backend";

export async function fetchRevenue() {
	// Add noStore() here to prevent the response from being cached.
	// This is equivalent to in fetch(..., {cache: 'no-store'}).
	noStore();
	try {
		const endpoint = `/api/revenue`;
		console.log(endpoint)
		const res = await backendClient.backend_get(endpoint,{cache: 'no-store'});
		console.log(res)
		const data = res.json()
		return data;
	} catch (error) {
		console.error('Fetch Revenue Error:', error);
		// throw new Error('Failed to fetch revenue data.');
	}
}

export async function fetchLatestInvoices() {
	noStore();
	try {
		const endpoint = `/api/invoice`;
		const res = await backendClient.backend_get(endpoint,{cache: 'no-store'});
		const latestInvoices = res.json()
		// console.log(latestInvoices)
		return latestInvoices;
	} catch (error) {
		console.error('Fetch invoices Error:', error);
		// throw new Error('Failed to fetch the latest invoices.');
	}
}

export async function fetchCardData() {
	return [{
		id: 1,
		title: "Total Users",
		number: 10.928,
		change: 12,
	},
		{
			id: 2,
			title: "Stock",
			number: 8.236,
			change: -2,
		},
		{
			id: 3,
			title: "Revenue",
			number: 6.642,
			change: 18,
		}]
}

const ITEMS_PER_PAGE = 6;

export async function fetchFilteredInvoices(
	query: string,
	currentPage: number,
) {
	noStore();
	const offset = (currentPage - 1) * ITEMS_PER_PAGE;

	try {
		const invoices = await sql<InvoicesTable>`
      SELECT
        invoices.id,
        invoices.amount,
        invoices.date,
        invoices.status,
        customers.name,
        customers.email,
        customers.image_url
      FROM invoices
      JOIN customers ON invoices.user_id = customers.id
      WHERE
        customers.name ILIKE ${`%${query}%`} OR
        customers.email ILIKE ${`%${query}%`} OR
        invoices.amount::text ILIKE ${`%${query}%`} OR
        invoices.date::text ILIKE ${`%${query}%`} OR
        invoices.status ILIKE ${`%${query}%`}
      ORDER BY invoices.date DESC
      LIMIT ${ITEMS_PER_PAGE} OFFSET ${offset}
    `;

		return invoices.rows;
	} catch (error) {
		console.error('Database Error:', error);
		throw new Error('Failed to fetch invoices.');
	}
}

export async function fetchInvoicesPages(query: string) {
	noStore();
	try {
		const count = await sql`SELECT COUNT(*)
    FROM invoices
    JOIN customers ON invoices.user_id = customers.id
    WHERE
      customers.name ILIKE ${`%${query}%`} OR
      customers.email ILIKE ${`%${query}%`} OR
      invoices.amount::text ILIKE ${`%${query}%`} OR
      invoices.date::text ILIKE ${`%${query}%`} OR
      invoices.status ILIKE ${`%${query}%`}
  `;

		const totalPages = Math.ceil(Number(count.rows[0].count) / ITEMS_PER_PAGE);
		return totalPages;
	} catch (error) {
		console.error('Database Error:', error);
		throw new Error('Failed to fetch total number of invoices.');
	}
}

export async function fetchInvoiceById(id: string) {
	noStore();
	try {
		const data = await sql<InvoiceForm>`
      SELECT
        invoices.id,
        invoices.user_id,
        invoices.amount,
        invoices.status
      FROM invoices
      WHERE invoices.id = ${id};
    `;

		const invoice = data.rows.map((invoice) => ({
			...invoice,
			// Convert amount from cents to dollars
			amount: invoice.amount / 100,
		}));

		return invoice[0];
	} catch (error) {
		console.error('Database Error:', error);
		throw new Error('Failed to fetch invoice.');
	}
}

export async function fetchCustomers() {
	try {
		const data = await sql<CustomerField>`
      SELECT
        id,
        name
      FROM customers
      ORDER BY name ASC
    `;

		const customers = data.rows;
		return customers;
	} catch (err) {
		console.error('Database Error:', err);
		throw new Error('Failed to fetch all customers.');
	}
}

export async function fetchFilteredCustomers(query: string) {
	noStore();
	try {
		const data = await sql<CustomersTableType>`
		SELECT
		  customers.id,
		  customers.name,
		  customers.email,
		  customers.image_url,
		  COUNT(invoices.id) AS total_invoices,
		  SUM(CASE WHEN invoices.status = 'pending' THEN invoices.amount ELSE 0 END) AS total_pending,
		  SUM(CASE WHEN invoices.status = 'paid' THEN invoices.amount ELSE 0 END) AS total_paid
		FROM customers
		LEFT JOIN invoices ON customers.id = invoices.user_id
		WHERE
		  customers.name ILIKE ${`%${query}%`} OR
        customers.email ILIKE ${`%${query}%`}
		GROUP BY customers.id, customers.name, customers.email, customers.image_url
		ORDER BY customers.name ASC
	  `;

		const customers = data.rows.map((customer) => ({
			...customer,
			total_pending: formatCurrency(customer.total_pending),
			total_paid: formatCurrency(customer.total_paid),
		}));

		return customers;
	} catch (err) {
		console.error('Database Error:', err);
		throw new Error('Failed to fetch customer table.');
	}
}

export async function getUser(email: string) {
	try {
		const user = await sql`SELECT * FROM users WHERE email=${email}`;
		return user.rows[0] as User;
	} catch (error) {
		console.error('Failed to fetch user:', error);
		throw new Error('Failed to fetch user.');
	}
}
