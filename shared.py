import time


def now():
    return time.perf_counter()


tables = {
    "actor_states": "height,head,code,state",
    "actors": "height,id,state_root,code,head,balance,nonce",
    "block_headers": "height,cid,miner,parent_weight,parent_base_fee,parent_state_root,win_count,timestamp,fork_signaling",
    "block_messages": "height,block,message",
    "block_parents": "height,block,parent",
    "chain_economics": "parent_state_root,circulating_fil,vested_fil,mined_fil,burnt_fil,locked_fil",
    "chain_powers": "height,state_root,total_raw_bytes_power,total_qa_bytes_power,total_raw_bytes_committed,total_qa_bytes_committed,total_pledge_collateral,qa_smoothed_position_estimate,qa_smoothed_velocity_estimate,miner_count,participating_miner_count",
    "chain_rewards": "height,state_root,cum_sum_baseline,cum_sum_realized,effective_baseline_power,new_baseline_power,new_reward_smoothed_position_estimate,new_reward_smoothed_velocity_estimate,total_mined_reward,new_reward,effective_network_time",
    "derived_gas_outputs": 'height,cid,state_root,"from","to",value,gas_fee_cap,gas_premium,gas_limit,size_bytes,nonce,method,actor_name,exit_code,gas_used,parent_base_fee,base_fee_burn,over_estimation_burn,miner_penalty,miner_tip,refund,gas_refund,gas_burned',
    "drand_block_entries": "round,block",
    "id_addresses": "id,address,state_root",
    "market_deal_proposals": "height,deal_id,state_root,padded_piece_size,unpadded_piece_size,start_epoch,end_epoch,client_id,provider_id,client_collateral,provider_collateral,storage_price_per_epoch,piece_cid,is_verified,label",
    "market_deal_states": "height,deal_id,sector_start_epoch,last_update_epoch,slash_epoch,state_root",
    "message_gas_economy": "height,state_root,base_fee,base_fee_change_log,gas_limit_total,gas_limit_unique_total,gas_fill_ratio,gas_capacity_ratio,gas_waste_ratio",
    "messages": 'height,cid,"from","to",value,gas_fee_cap,gas_premium,gas_limit,size_bytes,nonce,method',
    "miner_current_deadline_infos": "height,miner_id,state_root,deadline_index,period_start,open,close,challenge,fault_cutoff",
    "miner_infos": "height,miner_id,state_root,owner_id,worker_id,new_worker,worker_change_epoch,consensus_faulted_elapsed,peer_id,control_addresses,multi_addresses",
    "miner_fee_debts": "height,miner_id,state_root,fee_debt",
    "miner_locked_funds": "height,miner_id,state_root,locked_funds,initial_pledge,pre_commit_deposits",
    "miner_pre_commit_infos": "height,miner_id,sector_id,state_root,sealed_cid,seal_rand_epoch,expiration_epoch,pre_commit_deposit,pre_commit_epoch,deal_weight,verified_deal_weight,is_replace_capacity,replace_sector_deadline,replace_sector_partition,replace_sector_number",
    "miner_sector_deals": "height,miner_id,sector_id,deal_id",
    "miner_sector_events": "height,miner_id,sector_id,state_root,event",
    "miner_sector_infos": "height,miner_id,sector_id,state_root,sealed_cid,activation_epoch,expiration_epoch,deal_weight,verified_deal_weight,initial_pledge,expected_day_reward,expected_storage_pledge",
    "miner_sector_posts": "height,miner_id,sector_id,post_message_cid",
    "multisig_transactions": 'multisig_id,state_root,height,transaction_id,"to",value,method,params,approved',
    "multisig_approvals": 'height,state_root,multisig_id,message,method,approver,threshold,initial_balance,signers,gas_used,transaction_id,"to",value',
    "parsed_messages": 'height,cid,"from","to",value,method,params',
    "power_actor_claims": "height,miner_id,state_root,raw_byte_power,quality_adj_power",
    "receipts": "height,message,state_root,idx,exit_code,gas_used",
    'visor_processing_reports'     : 'height,state_root,reporter,task,started_at,completed_at,status,status_information,errors_detected'
}
