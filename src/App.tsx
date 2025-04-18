import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import './styles/global.css';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Content>
          <Routes>
            {/* 여기에 라우트를 추가할 예정 */}
            <Route path="/" element={<div>홈 페이지</div>} />
          </Routes>
        </Content>
      </Layout>
    </Router>
  );
};

export default App; 