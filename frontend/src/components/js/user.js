import { Button, Input, Table } from 'antd';
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from '../../context/AuthContext';
import useAxios from "../../utils/useAxios";


export default function User(){
    const api = useRef(useAxios())
    const { Search } = Input;
    let navigate = useNavigate()
    const [users, setUsers] = useState([])
    const [totalRecord , setTotalRecord] = useState(0)
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const {messageApi} = useContext(AuthContext)
    const [filterDict, setFilterDict] =useState({page:1,pageSize:10,orderBy:"-id",search:""})


    let getUserData = useCallback(async () =>{
        await api.current.get(`/qr_admin/user_list/?page=${filterDict.page}&page_size=${filterDict.pageSize}&ordering=${filterDict.orderBy}&search=${filterDict.search}`,
            )
            .then((res)=>{
                setTotalRecord(res.data.count)
                setUsers(res.data.results)
            })
            .catch((error)=>{
                messageApi.open({type: 'error',content: error.message})
            })
    },[filterDict, messageApi])

    useEffect(()=>{
        getUserData();
    }, [getUserData])


    const columns = [
        {title:"Name",dataIndex:"full_name",sorter: true},
        {title:"Mobile No.",dataIndex:"mobile",sorter: true},
        {title:"Address",dataIndex:"address",sorter: true},
        {title:"Pin Code",dataIndex:"pin_code",sorter: true},
        {title:"City",dataIndex:"city__name", sorter: true},
        {title:"State",dataIndex:"state__name",sorter: true},
        {title:"Distributor",dataIndex:"distributor__name",sorter: true},
    ]

    const onSelectChange =(newSelectedRowKeys)=>{
        setSelectedRowKeys(newSelectedRowKeys)
    }
    const viewWallet =()=>{
        if(selectedRowKeys.length !== 1){
            messageApi.open({type: 'error',content: "Please select one user."});
            return
        }
        else{
            navigate(`user_wallet/${selectedRowKeys}`)
            // navigate(`/user_wallet/${selectedRowKeys}`, {state:{selectedRowKeys:selectedRowKeys}})
            // this value can get using useLocation()
        }
    }

    const onTableChange = (pagination, filters, sorter) =>{
        var orderBy = sorter.order ? (sorter.order === "ascend"? "":"-") + sorter.field : "-id"
        setFilterDict({...filterDict,page:pagination.current,pageSize:pagination.pageSize,orderBy:orderBy})
    }

    return(
    <>
       <div className='title_tab'>
            <div className='title_tab_title'>Bond Users</div>
            <div className="title_tab_div">
                <Search placeholder="Search by mobile, name" allowClear={true} onChange={(e)=> {if(e.target.value===""){setFilterDict({...filterDict, search:""})}}} onSearch={(value) => setFilterDict({...filterDict, search:value})} style={{ width: 200 }} />
                <Button type="primary" onClick={viewWallet}>View Wallet</Button>
            </div>
        </div>
        <div className='main_tab'>
        <Table
            columns={columns}
            dataSource={users} rowKey="id"
            onChange={onTableChange}
            rowSelection={{selectedRowKeys,onChange: onSelectChange}}
            pagination={{total: totalRecord,
                defaultPageSize: 10, showSizeChanger: true,
                pageSizeOptions: ['10', '20', '50', '100'],
            }}
            footer={() => ( <div style={{textAlign:'right'}}>Selected Records ({selectedRowKeys.length} of {totalRecord})</div>)}
            scroll={{ x: '75pc' }}
            size="small"/>
        </div>
    </>
    )
}
