import { Card, Col, Progress, Row } from 'antd';
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from '../../context/AuthContext';
import useAxios from '../../utils/useAxios';
import batch_img from "../images/batch.png";
import qr_code_img from "../images/qr-code.png";
import user_img from "../images/user.png";



export default function CompanyDashBoard(){
    const api = useRef(useAxios())
    const [dashboard, setDashBoard] = useState({})
    const {messageApi} = useContext(AuthContext)

    const getDashBoardData = useCallback(async() =>{
        await api.current.get('/qr_admin/company_dashboard/')
        .then((res)=>{
            setDashBoard(res.data.data)
        })
        .catch((error)=>{
            messageApi.open({type: 'error',content: error.message})
        })
    },[messageApi])


    useEffect(()=>{
        getDashBoardData()
    },[getDashBoardData])

    return(
        <>
        <div className='title_tab'>
            <div className='title_tab_title'>Dashboard</div>
        </div>
        <div className='main_tab'>
            <Row>
                <Col span={8}>
                    <Card title="Total User" bordered={true}>
                        <img src={user_img} alt="user.png" style={{width:"50px", marginRight: '15px' }}></img>
                        <p><b>{dashboard.total_bond_user}</b></p>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Total Batch" bordered={true}>
                        <img src={batch_img} alt="batch.png" style={{width:"50px", marginRight: '15px' }}></img>
                        <p><b>{dashboard.total_qr_batch}</b></p>
                    </Card>
                </Col>
                <Col span={8}>
                    <Card title="Total QR Code" bordered={true}>
                        <img src={qr_code_img} alt="qr-code.png" style={{width:"50px", marginRight: '15px' }}></img>
                         <p><b>{dashboard.total_qr_code}</b></p>
                    </Card>
                </Col>
            </Row>
            <Row >
                <Card title="Used QR Code" bordered={true}>
                    <div style={{display:'Flex'}}>
                        <div><Progress type="circle" percent={dashboard.used_in_percentage} strokeColor={{'0%': '#108ee9','100%': '#87d068'}} /></div>
                        <div style={{padding: '12px 7px 0px 58px'}}>
                            <table><tbody>
                                    <tr><td><b>{dashboard.total_used_qr}</b></td><td>Used code</td></tr>
                                    <tr><td><b>{dashboard.total_remain_qr}</b></td><td>Remain code</td></tr>
                                    <tr><td colSpan="2"><hr></hr></td></tr>
                                    <tr><td><b>{dashboard.total_qr_code}</b></td><td>Total code</td></tr>
                            </tbody></table>
                        </div>
                    </div>
                </Card>
            </Row>
        </div>
        </>
    )
}