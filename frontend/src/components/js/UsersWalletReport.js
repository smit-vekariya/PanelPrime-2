import { Button, Input, Table } from "antd";
import React, { useCallback, useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import useAxios from "../../utils/useAxios";

export default function UsersWalletReport(){
    const api = useRef(useAxios())
    const { Search } = Input;
    const [walletData , setWalletData] = useState([])
    const [totalRecord , setTotalRecord] = useState(0)
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const {messageApi} = useContext(AuthContext)
    const filter_dict = {page:1,pageSize:10,orderBy:"-balance",search:"",top:0}
    const [filterDict, setFilterDict] =useState(filter_dict)

    const getUsersWalletData = useCallback(async() =>{
        await api.current.get(`/qr_admin/users_wallet_report/?page=${filterDict.page}&page_size=${filterDict.pageSize}&ordering=${filterDict.orderBy}&search=${filterDict.search}&top=${filterDict.top}`,
        )
        .then((res)=>{
            setTotalRecord(res.data.count)
            setWalletData(res.data.results)
        })
        .catch((error)=>{
            messageApi.open({type: 'error', content:error.message})
        })

    },[filterDict, messageApi])

    useEffect(()=>{
        getUsersWalletData()
    },[getUsersWalletData])

    const columns = [
        {title:"User", dataIndex:"user__mobile", sorter: true},
        {title:"Balance (₹)", dataIndex:"balance", sorter: true},
        {title:"Withdraw Balance (₹)", dataIndex:"withdraw_balance", sorter: true},
        {title:"Point", dataIndex:"point", sorter: true},
        {title:"Withdraw Point", dataIndex:"withdraw_point", sorter: true}
    ]

    const LoadFilter = ()=>{
       var top = document.getElementById("top_id").value
       var select_value = document.getElementById("select_value").value
       var orderBy = "-balance"
       if(select_value === "highest_balance"){
            orderBy = "-balance"
       }else if(select_value === "lowest_balance"){
            orderBy = "balance"
       }else if(select_value === "highest_withdraw"){
            orderBy = "-withdraw_balance"
       }else if(select_value === "Lowest_withdraw"){
            orderBy = "withdraw_balance"
       }
       setFilterDict({...filterDict,top:top,orderBy:orderBy})
    }

    const onReset =()=>{
        document.getElementById("top_id").value = 0
        document.getElementById("select_value").value = "highest_balance"
        setFilterDict(filter_dict)
    }

    const onSelectChange =(newSelectedRowKeys)=>{
        setSelectedRowKeys(newSelectedRowKeys)
    }

    const onTableChange = (pagination, filters, sorter) =>{
        var orderBy = sorter.order ? (sorter.order === "ascend"? "":"-") + sorter.field : "-id"
        setFilterDict({...filterDict,page:pagination.current,pageSize:pagination.pageSize,orderBy:orderBy})
    }
    return(
        <>
            <div className='title_tab'>
                <div className='title_tab_title'>Users Wallet Report</div>
                <div className="title_tab_div">
                    <Search placeholder="Search by user" allowClear={true} onChange={(e)=> {if(e.target.value===""){setFilterDict({...filterDict, search:""})}}} onSearch={(value) => setFilterDict({...filterDict, search:value})} style={{ width: 200 }} />
                </div>
            </div>
            <div className='report_tab'>
                <div>
                    <label>Top <input type="number" id="top_id" min={0} defaultValue="0" placeholder="" />
                        <select name="balance" id="select_value">
                            <option value="highest_balance">Highest Balance</option>
                            <option value="lowest_balance">Lowest Balance</option>
                            <option value="highest_withdraw">Highest Withdraw</option>
                            <option value="Lowest_withdraw">Lowest Withdraw</option>
                        </select>
                    </label>
                   <Button type="primary" onClick={LoadFilter}>Load</Button>
                   <Button onClick={onReset}>Reset</Button>
                </div>
                {/* <div>
                   <Button type="primary">Export</Button>
                </div> */}
            </div>
            <div className='main_tab'>
                <Table
                    columns={columns}
                    dataSource={walletData} rowKey="id"
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