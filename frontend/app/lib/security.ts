import { createHash } from 'crypto';


export const hashPassword = (data: string): string => {
	return createHash('sha256').update(data).digest('hex');
};
