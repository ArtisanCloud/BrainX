import useSettingsStore from "@/app/store/setting";

const ProvidersList: React.FC = () => {
  const { providers } = useSettingsStore(); // 获取 providers

  // 检查 providers 是否为空或未定义
  if (!providers || Object.keys(providers).length === 0) {
    return <div>No providers available</div>; // 如果没有 providers，显示提示
  }

  return (
    <div>
      {Object.entries(providers).map(([key, provider]) => (
        <div key={key}>
          <h3>{provider.provider}</h3>
          <p>{provider.description}</p>
        </div>
      ))}
    </div>
  );
};

export default ProvidersList;
