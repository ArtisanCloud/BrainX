import { BeakerIcon } from '@heroicons/react/24/outline';
import { noto_serif } from '@/app/styles/fonts';

export default function ArtisanCloudLogo() {
	return (
		<div
			className={`${noto_serif.className} border-0 flex flex-row items-center leading-none text-white`}
		>
			<BeakerIcon className="h-12 w-12" />
			<p className="text-[48px]">BrainX</p>
		</div>
	);
}