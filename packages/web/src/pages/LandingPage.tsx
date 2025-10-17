import React from 'react';
import { useNavigate } from 'react-router-dom';
import CardDemo from '../components/CardDemo';
import Button from '../components/Button';
import {
  PiChatsCircle,
  PiRobot,
} from 'react-icons/pi';
import AwsIcon from '../assets/aws.svg?react';
import {
  ChatPageQueryParams,
} from '../@types/navigate';
import queryString from 'query-string';


const agentCoreEnabled: boolean =
  import.meta.env.VITE_APP_AGENT_CORE_ENABLED === 'true';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const demoChat = () => {
    const params: ChatPageQueryParams = {
      content: 'AgentCoreとの対話テストです。こんにちは！',
      systemContext: '',
    };
    navigate(`/chat?${queryString.stringify(params)}`);
  };

  const demoAgentCore = () => {
    navigate(`/agent-core`);
  };

  return (
    <div className="pb-24">
      <div className="bg-aws-squid-ink flex flex-col items-center justify-center px-3 py-5 text-xl font-semibold text-white lg:flex-row">
        <AwsIcon className="mr-5 size-20" />
        AgentCore 対話インターフェース
      </div>

      <div className="mx-3 mb-6 mt-5 flex flex-col items-center justify-center text-xs lg:flex-row">
        <Button className="mb-2 mr-0 lg:mb-0 lg:mr-2" onClick={() => {}}>
          試す
        </Button>
        をクリックしてAgentCoreとの対話を開始できます。
      </div>

      <h1 className="mb-6 flex justify-center text-2xl font-bold">
        対話機能
      </h1>

      <div className="mx-4 grid gap-x-20 gap-y-5 md:grid-cols-1 xl:mx-20 xl:grid-cols-2">
        <CardDemo
          label="基本チャット"
          onClickDemo={demoChat}
          icon={<PiChatsCircle />}
          description="AgentCoreと基本的なチャット形式で対話することができます。"
        />
        {agentCoreEnabled && (
          <CardDemo
            label="AgentCore"
            onClickDemo={demoAgentCore}
            icon={<PiRobot />}
            description="AgentCoreの高度な機能を利用した対話が可能です。"
          />
        )}
      </div>
    </div>
  );
};

export default LandingPage;
