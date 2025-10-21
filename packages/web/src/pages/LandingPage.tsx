import React from 'react';
import { useNavigate } from 'react-router-dom';
import CardDemo from '../components/CardDemo';
import Button from '../components/Button';
import { PiRobot } from 'react-icons/pi';
import AwsIcon from '../assets/aws.svg?react';
import { useTranslation } from 'react-i18next';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="pb-24">
      <div className="bg-aws-squid-ink flex h-48 w-full flex-col items-center justify-center text-4xl text-white lg:h-64">
        <div className="flex items-center">
          <AwsIcon className="mr-5 h-20 w-20 fill-white lg:h-28 lg:w-28" />
          <div>
            <div className="text-base font-bold lg:text-xl">
              {t('landing.title')}
            </div>
            <div className="text-3xl font-bold lg:text-5xl">
              {t('landing.subtitle')}
            </div>
          </div>
        </div>
      </div>

      <div className="mx-3 my-10 flex flex-col items-center justify-center lg:mx-20">
        <div className="w-full max-w-5xl">
          <div className="mb-5 text-xl font-bold">AgentCore</div>

          <div className="grid grid-cols-1 gap-3 lg:grid-cols-2">
            <CardDemo
              label="AgentCore Chat"
              icon={<PiRobot />}
              description="Amazon Bedrock AgentCore を使用したチャット機能"
              onClickDemo={() => navigate('/agent-core')}
            />
          </div>
        </div>

        <div className="mt-20 flex w-full max-w-5xl flex-col items-center justify-center">
          <Button
            className="w-full lg:w-96"
            onClick={() => {
              navigate('/setting');
            }}>
            {t('landing.settingsButton')}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
