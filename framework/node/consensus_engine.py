#!/usr/bin/env python3
"""
Zero-Point Protocol — Fluid Spectral Consensus Loop
Decentralized validation for un-sandboxed internet ingress telemetry.
"""
import asyncio
from typing import Dict, List, Any
from evaluation import EvaluationResult
from scoring import GammaScorer

class ConsensusEngine:
    def __init__(self, node_id: str, cluster_weights: Dict[str, float]):
        self.node_id = node_id
        # Runtime fluid authority map: initialized from config, managed in memory
        self.weights = dict(cluster_weights)  # {"NODE_A": 0.33, "NODE_B": 0.33, "NODE_C": 0.34}
        self.variance_threshold = 0.05
        
    def _calculate_mean(self, data: List[float]) -> float:
        return sum(data) / len(data) if data else 0.0

    def _calculate_variance(self, data: List[float]) -> float:
        if not data:
            return 1.0
        mean = self._calculate_mean(data)
        return sum((x - mean) ** 2 for x in data) / len(data)

    async def evaluate_ingress_vector(
        self, 
        text: str, 
        context: List[Any], 
        peer_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Executes decentralized validation loop without an orchestrator.
        Compares local scoring calculations against active peer responses.
        """
        # Step 1: Compute localized Gamma scoring matrix
        scorer = GammaScorer(weights=None)  # Uses ZPP standard heuristics
        local_res = scorer.evaluate(text, context=context)
        
        # Inject our score into the shared peer dictionary via web socket message
        peer_scores[self.node_id] = local_res.gamma_score
        
        # Step 2: Extract active validation scores from the 3 consensus nodes
        active_keys = ["NODE_A", "NODE_B", "NODE_C"]
        active_scores = [peer_scores[k] for k in active_keys if k in peer_scores]
        
        if len(active_scores) < 3:
            return {
                "status": "AWAITING_PEERS", 
                "local_score": local_res.gamma_score,
                "current_pool": list(peer_scores.keys())
            }
            
        # Step 3: Run Convergence Test via Spectral Variance
        variance = self._calculate_variance(active_scores)
        mean_score = self._calculate_mean(active_scores)
        is_converged = variance <= self.variance_threshold
        
        if is_converged:
            # Mathematical invariant achieved. Inform transport layer to register state hash.
            return {
                "status": "CONVERGED",
                "variance": round(variance, 6),
                "consensus_score": round(mean_score, 4),
                "action": "REGISTER_LATTICE_STATE",
                "gamma_lock": mean_score >= scorer.gamma_threshold
            }
        else:
            # Volatility detected. Identify the outlier node causing alignment drift.
            outlier_node = max(
                active_keys, 
                key=lambda k: abs(peer_scores.get(k, mean_score) - mean_score)
            )
            return {
                "status": "DIVERGENT",
                "variance": round(variance, 6),
                "action": "MUTATE_FLUID_WEIGHTS",
                "outlier_target": outlier_node
            }

    def mutate_weights(self, outlier_node: str, penalty_factor: float = 0.05):
        """
        Dynamically shifts weight distribution away from divergent nodes.
        Ensures the collective authority always re-normalizes exactly to 1.0.
        """
        active_keys = ["NODE_A", "NODE_B", "NODE_C"]
        if outlier_node not in active_keys:
            return

        # Deduct authority from the divergent outlier
        current_outlier_w = self.weights[outlier_node]
        clamped_penalty = min(penalty_factor, current_outlier_w - 0.10) # Keep weight >= 0.10
        
        if clamped_penalty <= 0:
            return  # Lower limit boundary constraint reached
            
        self.weights[outlier_node] -= clamped_penalty
        
        # Share the structural bonus equally among the remaining aligned nodes
        aligned_nodes = [k for k in active_keys if k != outlier_node]
        bonus_share = clamped_penalty / len(aligned_nodes)
        
        for node in aligned_nodes:
            self.weights[node] += bonus_share
            
        # Verify precision rounding matches absolute 1.0 baseline
        total = sum(self.weights[k] for k in active_keys)
        if not abs(total - 1.0) < 1e-6:
            # Re-normalize cleanly
            for k in active_keys:
                self.weights[k] /= total
