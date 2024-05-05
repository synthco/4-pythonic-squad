import { Alarm } from "./Alarm";

type Props = {
  alarms: object
}

export const Region = ({ alarms }: Props) => {

  return <div>
    {Object.entries(alarms).map(([time, isAlarm]) => (
      <Alarm key={time} time={time} isAlarm={isAlarm} />
    ))}
  </div>;
}
