import { createHash } from 'crypto';


export const encodePassword = (data: string): string => {
	return createHash('sha256').update(data).digest('hex');
};
