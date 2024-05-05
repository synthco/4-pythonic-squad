type Props = {
  time: string
  isAlarm: boolean
}

export const Alarm = ({ time, isAlarm }: Props) => {
  return <div style={{ color: isAlarm ? '#FA5F55' : '#50C878' }}>{time}</div>;
}
