import { ReactNode, useState } from 'react';

type Props = {
  title: string
  children: ReactNode
}

export const Accordion = ({ title, children }: Props) => {
  const [isActive, setIsActive] = useState(false);

  return (
    <div className="accordion-item">
      <div className="accordion-title" onClick={() => setIsActive(!isActive)}>
        <div>{title}</div>
        <div>{isActive ? '-' : '+'}</div>
      </div>
      {isActive && <div className="accordion-content">{children}</div>}
    </div>
  );
};
